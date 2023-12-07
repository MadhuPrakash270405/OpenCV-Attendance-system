// Initialize DataTable
new DataTable("#example");
let globalStream = null; // Ensure this is globally accessible

// AJAX function for API calls
async function ajax_function(api_endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {}
    };

    if (method === 'POST' && data) {
        options.headers['Content-Type'] = 'application/json';
        options.body = JSON.stringify(data);
    }

    const response = await fetch(api_endpoint, options);
    if (!response.ok) {
        throw new Error("Network response was not ok");
    }
    return await response.text();
}

// Function to handle webcam start/stop
function handleOpenCVFrameStartStop(start) {
    console.log(start ? "starting-webcam" : "stopping-webcam");
    ajax_function(start ? "/start-webcam" : "/stop-webcam");
}

// Function to start webcam streaming
function handleWebcamStart() {
    console.log("starting-webcam");
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } })
            .then(stream => {
                globalStream = stream;
                const video = document.getElementById('webcam_video');
                video.srcObject = stream;
                video.play();
            })
            .catch(error => console.error("Webcam error:", error));
    }
}


function stopWebcam() {
    try {
        if (globalStream && typeof globalStream.getTracks === 'function') {
            globalStream.getTracks().forEach(track => track.stop());
            globalStream = null;
            const videoElement = document.getElementById('webcam_video');
            if (videoElement) {
                videoElement.srcObject = null;
            } else {
                console.error("stopWebcam: Video element not found");
            }
        } else {
            console.error("stopWebcam called but globalStream is not a MediaStream or getTracks is not a function");
        }
    } catch (error) {
        console.error("stopWebcam: An error occurred", error);
    }
}


// Function to handle student ID input
function handleStudentIdInput(studentId) {
    const successMsg = document.getElementById("registration_success_message");
    const errorText = document.getElementById("registration_error");

    successMsg.textContent = "";
    errorText.textContent = "";
    if (studentId.value.length === 7 && !isNaN(studentId.value)) {
        ajax_function('/send-otp', 'POST', { 'student_id': studentId.value });
        successMsg.textContent = "OTP Sent to your email Successfully!";
        studentId.disabled = true;
        document.getElementById("registration_otp").disabled = false;
    } else if (studentId.value.length > 0) {
        errorText.textContent = "Please enter a numeric 7-digit code.";
    }
}

// Function to handle OTP input
function handleOtpInput(otpInput) {
    const otpSuccessMsg = document.getElementById("registration_otp_success_message");
    const otpErrorText = document.getElementById("registration_otp_error");
    const submitButton = document.getElementById("registration_submitButton");

    otpSuccessMsg.textContent = "";
    otpErrorText.textContent = "";
    if (otpInput.value.length === 6 && !isNaN(otpInput.value)) {
        ajax_function("/verify-otp", 'POST', { otp: otpInput.value, student_id: document.getElementById("registration_student_id").value })
            .then(data => {
                console.log('Success:', data);
                if (data === "Valid OTP.") {
                    otpSuccessMsg.textContent = "Valid OTP. You can now submit.";
                    submitButton.disabled = false;
                } else {
                    otpErrorText.textContent = "Invalid OTP. Please try again.";
                    submitButton.disabled = true;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                otpErrorText.textContent = "An error occurred while verifying OTP.";
                submitButton.disabled = true;
            });
    } else {
        otpErrorText.textContent = "Enter Valid 6-digit code.";
        submitButton.disabled = true;
    }
}

// Event listeners for DOM content loaded
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("start-webcam").addEventListener("click", () => handleOpenCVFrameStartStop(true));
    document.getElementById("stop-webcam").addEventListener("click", () => handleOpenCVFrameStartStop(false));
    document.getElementById("register_student_button").addEventListener("click", () => {
        handleWebcamStart();
        reinitializeRegistrationForm();
    });

    document.getElementById("registration_submitButton").addEventListener("click", handleStudentRegistration);
    document.getElementById("registration_close_button").addEventListener("click", stopWebcam);
    handleLogin()
});

function handleLogin() {
  const loginSubmitButton = document.getElementById("loginSubmitButton");
  const usernameInput = document.getElementById("username");
  const passwordInput = document.getElementById("password");
  passwordInput.addEventListener("input", () =>{
    if(username !=='' && password !=='') loginSubmitButton.disabled = false
  });
  
  loginSubmitButton.addEventListener("click", async function(event) {
      event.preventDefault(); // Prevent the form from submitting via the browser

      const username = usernameInput.value;
      const password = passwordInput.value;
     
      try {
          const response = await ajax_function('/login', 'POST', {
              username: username,
              password: password
          });

          // Handle the response here
          console.log("Login response:", response);
          if (response === "Login Sucessfull") {
            window.location.href = '/';
          }
      } catch (error) {
          console.error("Login failed:", error);
      }
  });
}
function reinitializeRegistrationForm() {
    const studentId = document.getElementById("registration_student_id");
    const otpCodeInput = document.getElementById("registration_otp");
    const registrationStatusSuccessMsg = document.getElementById("registration_status_success_message");
    const registrationStatusErrorMsg = document.getElementById("registration_status_error_message");
    const otpSuccessMsg = document.getElementById("registration_otp_success_message");
    const otpErrorText = document.getElementById("registration_otp_error");
    const successMsg = document.getElementById("registration_success_message");
    const errorText = document.getElementById("registration_error");

    studentId.value = '';
    otpCodeInput.value = '';
    studentId.disabled = false;
    otpCodeInput.disabled = true;
    registrationStatusSuccessMsg.textContent = '';
    registrationStatusErrorMsg.textContent = '';
    otpSuccessMsg.textContent = '';
    otpErrorText.textContent = '';
    successMsg.textContent = '';
    errorText.textContent = '';
    studentId.addEventListener("input", () => handleStudentIdInput(studentId));
    otpCodeInput.addEventListener("input", () => handleOtpInput(otpCodeInput));
}

function captureFace() {
    const video = document.getElementById('webcam_video');
    const canvas = document.createElement('canvas');
    canvas.width = 320;
    canvas.height = 240;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/png');
}

function handleStudentRegistration(event) {
    event.preventDefault();
    const studentId = document.getElementById("registration_student_id");
    ajax_function("/register-student", 'POST', { student_id: studentId.value, image: captureFace() })
        .then(data => {
            console.log('Success:', data);
            handleServerResponse(data);
        });
}

function handleServerResponse(data) {
    const registrationStatusSuccessMsg = document.getElementById("registration_status_success_message");
    const registrationStatusErrorMsg = document.getElementById("registration_status_error_message");
    data = JSON.parse(data);
    registrationStatusSuccessMsg.textContent = '';
    registrationStatusErrorMsg.textContent = '';

    if (data.message === "Student registered successfully") {
        registrationStatusSuccessMsg.textContent = data.message;

    } else {
        registrationStatusErrorMsg.textContent = data.message;
    }
    setTimeout(() => {
      window.location.reload();
  }, 3000);

}

new DataTable("#example");
function ajax_function(api_endpoint) {
  fetch(api_endpoint)
    .then((response) => {
      if (response.ok) {
        return response.text();
      } else {
        throw new Error("Something went wrong");
      }
    })
    .then((text) => {
      console.log(text);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

document.addEventListener("DOMContentLoaded", function () {
  var studentId = document.getElementById("student_id");
  var otpCodeInput = document.getElementById("otp");
  var submitButton = document.getElementById("submitButton");
  var errorText = document.getElementById("error");
  var successMsg = document.getElementById("success_message");
  var otpErrorText = document.getElementById("otp_error");
  var otpSuccessMsg = document.getElementById("otp_success_message");
  studentId.addEventListener("input", function () {
    var student_id = studentId.value;
    // Clear error message initially
    successMsg.textContent = "";
    errorText.textContent = "";
    // Check if the code is numeric and exactly 7 digits
    if (student_id.length === 7 && !isNaN(student_id)) {
      // Enable the submit button
      successMsg.textContent = "OTP Sent to your email Successfully!";
      //   submitButton.disabled = false;
    } else {
      // Disable the submit button and display an error message if the input is not valid
      //   submitButton.disabled = true;
      if (student_id.length > 0) {
        successMsg.textContent = "";
        errorText.textContent = "Please enter a numeric 7-digit code.";
      }
    }
  });
  otpCodeInput.addEventListener("input", function () {
    var otp = otpCodeInput.value;
    // Clear error message initially
    otpSuccessMsg.textContent = "";
    otpErrorText.textContent = "";
    // Check if the code is numeric and exactly 7 digits
    if (otp.length === 7 && !isNaN(otp)) {
      // Enable the submit button
      otpSuccessMsg.textContent = "OTP Verified Successfully!";
      submitButton.disabled = false;
    } else {
      // Disable the submit button and display an error message if the input is not valid
      submitButton.disabled = true;
      otpErrorText.textContent = "Enter Valid 7-digit code.";
      if (otp.length > 0) {
        otpErrorText.textContent = "Please enter a numeric 7-digit code.";
      }
    }
  });
});

document
  .getElementById("start-webcam")
  .addEventListener("click", function (event) {
    console.log("starting-webcam");
    event.preventDefault(); // Prevent default link behavior
    ajax_function("/start-webcam");
  });

document
  .getElementById("stop-webcam")
  .addEventListener("click", function (event) {
    console.log("stoping-webcam");
    event.preventDefault(); // Prevent default link behavior
    ajax_function("/stop-webcam");
  });

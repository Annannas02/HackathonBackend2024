function open_menu() {
  document.getElementById("menu").style.removeProperty("width");
  document.getElementById("menu-open-button").style.left = "-100px";
  document.getElementById("homepage-content-frame").style.removeProperty("margin-left");

}
function close_menu() {
  document.getElementById("menu").style.width = "0px";
  document.getElementById("menu-open-button").style.left = "16px";
  document.getElementById("homepage-content-frame").style.marginLeft = "0px";
}

function open_pop(pop) {
  const popElement = document.getElementById(pop);
  popElement.style.display = "flex";

  function close(e) {
    const menus = document.querySelectorAll(".pop__menu-frame");
    const buttons = document.querySelectorAll(".pop-button");

    const isClickOutsideButton = !Array.from(buttons).some(button => button.contains(e.target));
    const isClickOutsideMenu = !Array.from(menus).some(menu => menu.contains(e.target));

    if (isClickOutsideButton && isClickOutsideMenu) {
      close_pop(pop);
      document.removeEventListener('click', close);
    }
  }

  document.addEventListener('click', close);
}

function close_pop() {
  const settingsFrames = document.querySelectorAll(".pop-window");
  settingsFrames.forEach(frame => {
    frame.style.removeProperty("display");
  });
  document.removeEventListener('click', close);
}


function clear_input(input_name) {
  document.getElementById(input_name).value = "";
}
// Themes

function theme_midnight() {
  document.documentElement.style.setProperty('--main-color-1', '#121212');
  document.documentElement.style.setProperty('--main-color-2', '#1E1E1E');
  document.documentElement.style.setProperty('--main-color-3', '#E0E0E0');
  document.documentElement.style.setProperty('--main-color-4', '#3A3A3A');

  document.documentElement.style.setProperty('--hover-color-1', '#333333');
  document.documentElement.style.setProperty('--hover-color-2', '#121212d4');
  document.documentElement.style.setProperty('--dark-cover', '#000000d5');
  document.documentElement.style.setProperty('--input-color', '#FFFFFF');
}

function theme_default() {
  document.documentElement.style.setProperty('--main-color-1', '#F8EDE3');
  document.documentElement.style.setProperty('--main-color-2', '#D0B8A8');
  document.documentElement.style.setProperty('--main-color-3', '#3B3030');
  document.documentElement.style.setProperty('--main-color-4', '#DFD0C6');

  document.documentElement.style.setProperty('--hover-color-1', '#3b30302a');
  document.documentElement.style.setProperty('--hover-color-2', '#f8ede3be');
  document.documentElement.style.setProperty('--dark-cover', '#000000d5');
  document.documentElement.style.setProperty('--input-color', '#000000');

}

function theme_blossom() {
  document.documentElement.style.setProperty('--main-color-1', '#FEE3E3');
  document.documentElement.style.setProperty('--main-color-2', '#F5B2B2');
  document.documentElement.style.setProperty('--main-color-3', '#7A2A2A');
  document.documentElement.style.setProperty('--main-color-4', '#F5CFCF');

  document.documentElement.style.setProperty('--hover-color-1', '#F09A9A');
  document.documentElement.style.setProperty('--hover-color-2', '#FEE3E3d4');
  document.documentElement.style.setProperty('--dark-cover', '#000000d5');
  document.documentElement.style.setProperty('--input-color', '#3A3A3A');
}

function theme_forest() {
  document.documentElement.style.setProperty('--main-color-1', '#A8D5BA');
  document.documentElement.style.setProperty('--main-color-2', '#7B9A8D');
  document.documentElement.style.setProperty('--main-color-3', '#2F4C4B');
  document.documentElement.style.setProperty('--main-color-4', '#C6E4D6');

  document.documentElement.style.setProperty('--hover-color-1', '#6B9A8B');
  document.documentElement.style.setProperty('--hover-color-2', '#A8D5BAd4');
  document.documentElement.style.setProperty('--dark-cover', '#000000d5');
  document.documentElement.style.setProperty('--input-color', '#1A2420');

}
function theme_retro_pop() {
  document.documentElement.style.setProperty('--main-color-1', '#F5D491');
  document.documentElement.style.setProperty('--main-color-2', '#E28D74');
  document.documentElement.style.setProperty('--main-color-3', '#2C2F45');
  document.documentElement.style.setProperty('--main-color-4', '#F6E1B8');

  document.documentElement.style.setProperty('--hover-color-1', '#D67A63');
  document.documentElement.style.setProperty('--hover-color-2', '#F5D491d4');
  document.documentElement.style.setProperty('--dark-cover', '#000000d5');
  document.documentElement.style.setProperty('--input-color', '#2C2F45');


}
// Theme load

function apply_theme(theme) {
  switch (theme) {
    case "midnight":
      theme_midnight();
      break;
    case "blossom":
      theme_blossom();
      break;
    case "forest":
      theme_forest();
      break;
    case "retro-pop":
      theme_retro_pop();
      break;
    default:
      theme_default();
  }
  localStorage.setItem("theme", theme);
}

function load_theme() {
  const savedTheme = localStorage.getItem("theme") || "default";
  apply_theme(savedTheme);
  document.getElementById(`${savedTheme}-theme-check`).checked = true;
  document.removeEventListener('DOMContentLoaded', load_theme);
}

document.addEventListener('DOMContentLoaded', load_theme);


//-----



function open_output() {
  document.getElementById("output-frame").style.display = "flex";
  document.addEventListener('click', function close(e) {
    const outputbody = document.getElementById("output-body");
    const button = document.getElementById("email-generate-button");
    const button1 = document.getElementById("open-output-button");

    if (!outputbody.contains(e.target) && !button.contains(e.target) && !button1.contains(e.target)) {
      close_output();
    }
  });

}
function close_output() {
  document.getElementById("output-frame").style.removeProperty("display");
  document.removeEventListener('click', close);
}
function clipboard_copy() {
  text_value = document.getElementById("output-box").value;
  navigator.clipboard.writeText(text_value);
}

async function registerUser(username, password) {
  try {
      const response = await fetch("https://92f1-77-89-208-34.ngrok-free.app/api/authen/auth/register", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
          const errorData = await response.json();
          console.error("Registration failed:", errorData);
          alert(`Registration failed: ${errorData.message || "Unknown error"}`);
          return;
      }

      alert("Registration successful!");
  } catch (error) {
      console.error("Error during registration:", error);
      alert("An error occurred during registration. Please try again later.");
  }
}

function register_proxy() {
  const username = document.getElementById("input-name").value.trim();
  const password = document.getElementById("input-password").value.trim();

  if (!username || !password) {
      alert("Please fill in both fields.");
      return;
  }

  registerUser(username, password);
}

async function generateOtp(username, password) {
  try {
      const response = await fetch("https://92f1-77-89-208-34.ngrok-free.app/api/authen/2fa/generateOtp", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
          const errorData = await response.json();
          console.error("OTP generation failed:", errorData);
          alert(`Failed to generate OTP: ${errorData.message || "Unknown error"}`);
          return null;
      }

      const { totp_code } = await response.json();
      console.log("OTP generated successfully:", totp_code);
      return totp_code;
  } catch (error) {
      console.error("Error generating OTP:", error);
      alert("An error occurred while generating OTP. Please try again later.");
      return null;
  }
}

async function authenticateUser(username, otpCode) {
  try {
      const response = await fetch("https://92f1-77-89-208-34.ngrok-free.app/api/authen/2fa/authenticate", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify({ username, totp_code: otpCode }),
      });

      if (!response.ok) {
          const errorData = await response.json();
          console.error("Authentication failed:", errorData);
          alert(`Authentication failed: ${errorData.message || "Unknown error"}`);
          return null;
      }

      const tokens = await response.json();
      console.log("Authentication successful. Tokens:", tokens);
      return tokens;
  } catch (error) {
      console.error("Error during authentication:", error);
      alert("An error occurred during authentication. Please try again later.");
      return null;
  }
}

async function loginProxy() {
  const username = document.getElementById("input-name-login").value.trim();
  const password = document.getElementById("input-password-login").value.trim();

  if (!username || !password) {
      alert("Please fill in both fields.");
      return;
  }

  // Step 1: Generate OTP and authenticate
  const otpCode = await generateOtp(username, password);
  if (!otpCode) {
      return; // Stop if OTP generation failed
  }

  const tokens = await authenticateUser(username, otpCode);
  if (tokens) {
      // Step 2: Store tokens and proceed
      localStorage.setItem("access_token", tokens.access);
      localStorage.setItem("refresh_token", tokens.refresh);
      alert("Login successful!");
      console.log("Access Token:", tokens.access);
      console.log("Refresh Token:", tokens.refresh);

      // Redirect to a new page or update the UI to reflect login success
      window.location.href = "/"; // Replace with your desired page
  }
}
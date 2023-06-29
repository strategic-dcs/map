import './LoginPrompt.css';

function LoginPrompt() {
  return  <div className="lightbox-container">
      <div className="lightbox">
        <a href="https://discord.com/api/oauth2/authorize?client_id=1121891789096374382&redirect_uri=http://localhost:3000/auth/callback&scope=identify&response_type=code" className="login-link">
          Please Login on Discord
        </a>
      </div>
    </div>
}

export default LoginPrompt;

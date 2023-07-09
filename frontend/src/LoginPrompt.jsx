import './LoginPrompt.css';

function LoginPrompt() {
  const fqdn = import.meta.env.VITE_FQDN
  const discord_client_id = import.meta.env.VITE_DISCORD_CLIENT_ID
  const login_url = `https://discord.com/api/oauth2/authorize?client_id=${discord_client_id}` +
                    `&redirect_uri=${fqdn}/auth/callback&scope=identify&response_type=code`

  return  <div className="lightbox-container">
      <div className="lightbox">
        <a href={login_url} className="login-link">
          Please Login on Discord
        </a>
      </div>
    </div>
}

export default LoginPrompt;

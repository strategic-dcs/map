import { useEffect, useState } from 'react';
import './LoginPrompt.css';
import axios from 'axios';

function LoginPrompt() {
  const [discordLoginUrl, setDiscordLoginUrl] = useState(false)

  useEffect(() => {
    axios.get("/api/auth/discord_login_url").then((req) => {
      setDiscordLoginUrl(req.data.discord_login_url)
    })
  }, [discordLoginUrl])

  if (!discordLoginUrl) { return <div>Loading...</div>}

  return  <div className="lightbox-container">
    <div className="lightbox">
      <a href={discordLoginUrl} className="login-link">
        Please Login on Discord
      </a>
    </div>
  </div>
}

export default LoginPrompt;


import "./ServerInfo.css";

function convertSecondsToFormatedTime(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const formattedTime = `${hours}h${minutes}min`;
  return formattedTime;
}

export default function ServerInfo(props) {
  const online_users = props.online_users
  const seconds_left_until_restart = props.seconds_left_until_restart

  const red_users = online_users.filter((user) => { return user.coalition.toUpperCase() === "RED" })
  const blue_users = online_users.filter((user) => { return user.coalition.toUpperCase() === "BLUE" })

  const red_list = red_users
    .sort((user) => { return user.name })
    .map((user) => {
    return <li key={user.name}>{user.name}</li>
  })

  const blue_list = blue_users
    .sort((user) => { return user.name })
    .map((user) => {
    return <li key={user.name}>{user.name}</li>
  })

  return <div className="serverInfoContainer">
      <div className="content">
        <div className="header">
          <div className="blue">{blue_users.length}</div> vs <div className="red">{red_users.length}</div>
        </div>
        <div className="total">({blue_users.length + red_users.length} Pilots)</div>

        <div className="list">
          <ul className="blue">
            {blue_list}
          </ul>
          <ul className="red">
            {red_list}
          </ul>
        </div>
        <div className="line"></div>
        <div className="serverMinutes">
          <div>Total <div className="insert blue">BLUE</div> minutes played: <span className="">{props.blue_minutes_played}</span></div>
          <div>Total <div className="insert red">RED</div> minutes played: <span className="">{props.red_minutes_played}</span></div>
        </div>

        <div className="serverStats">
          <div>Server Restart in: {convertSecondsToFormatedTime(seconds_left_until_restart)}</div>
        </div>
      </div>
  </div>
}

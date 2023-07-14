

function convertSecondsToFormatedTime(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const formattedTime = `${hours}h${minutes}min`;
  return formattedTime;
}

export default function ServerInfo(props) {
  const online_users = props.online_users
  const seconds_left_until_restart = props.seconds_left_until_restart

  const red_users = online_users.filter((user) => { return user.coalition === "RED" })
  const blue_users = online_users.filter((user) => { return user.coalition === "BLUE" })

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
      <div className="serverStats">
        <div>Server Restart in: {convertSecondsToFormatedTime(seconds_left_until_restart)}</div>
      </div>
  </div>
}

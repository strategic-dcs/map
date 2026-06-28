
import "./ServerInfo.css";

function convertSecondsToFormatedTime(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const formattedTime = `${hours}h${minutes}min`;
  return formattedTime;
}

function formatDate(date) {
    var d = new Date(date)

		let month = '' + (d.getMonth() + 1);
    let day = '' + d.getDate();
		let year = d.getFullYear();

		let hour = '' + d.getHours();
		let minutes = '' + d.getMinutes();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;
    if (hour.length < 2)
        hour = '0' + hour;
    if (minutes.length < 2)
        minutes = '0' + minutes;


    return [year, month, day].join('-') + ' ' + [hour,minutes].join(':');
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
					<div></div>
					<div className="insert blue flex">BLUE</div>
					<div className="insert red flex">RED</div>

					<div className="flex">minutes played</div>
					<div className="flex"><span>{props.blue_minutes_played}</span></div>
					<div className="flex"><span>{props.red_minutes_played}</span></div>

					<div className="flex">minutes four hours</div>
					<div className="flex"><span>{props.blue_minutes_4h}</span></div>
					<div className="flex"><span>{props.red_minutes_4h}</span></div>

					<div className="flex">registered</div>
					<div className="flex"><span>{props.blue_registered}</span></div>
					<div className="flex"><span>{props.red_registered}</span></div>
        </div>

        <div className="serverStats">
          <div>Server Time: {formatDate(props.dcs_time)}</div>
        </div>

        <div className="serverStats">
          <div>Server Restart in: {convertSecondsToFormatedTime(seconds_left_until_restart)}</div>
        </div>
      </div>
  </div>
}

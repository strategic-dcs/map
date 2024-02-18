export function secondsToText(work) {

    let results = []

    let days = Math.floor(work / 86400)
    if (days > 0) results.push(`${days}d`)

    work %= 86400

    let hours = Math.floor(work / 3600)
    results.push(`${hours.toString().padStart(2, '0')}h`)
    work %= 3600

    let seconds = Math.floor(work / 60)
    results.push(`${seconds.toString().padStart(2, '0')}m`)

    return results.join("")

}
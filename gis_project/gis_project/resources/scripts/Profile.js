
function calcAverage(games_played, sum_of_points) {
    let points_per_game = "ERROR"
    if (games_played > 0 && sum_of_points > 0) {
        points_per_game = (sum_of_points / games_played).toString();
    } else {
        points_per_game = "Nothing to Display";
    }
    document.getElementById("points_per_game").innerHTML = points_per_game;
}

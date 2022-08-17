
/*
To get how many days left of school: 

Graduation date : 2022/5/20
Today's date : 2022/1/10
We subtract the days and exclude weekends and holidays

1) Get a list of weekends and holidays
2) Get todays date
3) Get end date
4) Calculate the number of days between today and end 
5) Subtract the length of weekend/holiday list 
6) Done!
*/

function countDaysLeft(end_date) {
  const today = new Date();

  numWeekends = getWeekends(end_date).length;
  numHolidays = getHolidays().length;
  daysLeft = getDaysBetween(today, end_date) - (numWeekends + numHolidays);
  return daysLeft
}

function getDaysBetween(start_date, end_date) {
  var time_dif = end_date.getTime() - start_date.getTime();
  var day_dif = Math.round(time_dif / (1000 * 3600 * 24))
  return day_dif;
}

function getWeekends(end_date) {
  w = [] // weekends
  current_date = new Date();
  while(current_date < end_date) {
    const sunday = endOfWeek(current_date);
    const saturday = addDays(sunday, -1);
    w.push(saturday)
    w.push(sunday)
    current_date = addDays(sunday, 1);
  }

  return w;
}

function getHolidays() {
  const holidays = [
    new Date(2022, 1, 17), // MLK day
    new Date(2022, 2, 21), // President's day
    new Date(2022, 3, 28), //Spring break
    new Date(2022, 3, 29), //Spring break
    new Date(2022, 3, 30), //Spring break
    new Date(2022, 3, 31), //Spring break
    new Date(2022, 4, 1), // Spring break
    new Date(2022, 4, 15), // Non attendance day
    // new Date(2022, 5, 30), // Memorial Day
    ];
  return holidays
}

function endOfWeek(date)
  {
    // Returns Sunday of the current week
    var lastday = date.getDate() - (date.getDay() - 1) + 6;
    return new Date(date.setDate(lastday));
 
  }

function addDays(date, value) {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate() + value);
}

const endDate = new Date(2022, 5, 20);
const d = countDaysLeft(endDate)
document.getElementById("countdown").textContent = d + " days left of school!";





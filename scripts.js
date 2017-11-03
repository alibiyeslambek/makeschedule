var courseNumber = 0;
var addCourseButton = document.getElementById('add-course-button').addEventListener("click", addCourse);

function addCourse() {
	courseNumber++;
	var courseList = document.getElementById('course-list');
	var courseRow = document.createElement('div');
	courseRow.setAttribute("class", "row");
	

	var courseColumn = document.createElement('div');
	courseColumn.setAttribute("class", "col-xs-4");
	courseColumn.innerHTML += 'Course Title: <input type = "text" name = "course' +  courseNumber + '"> <br>';

	var timeColumn = document.createElement('div');
	timeColumn.setAttribute("class", "col-xs-6");

	var buttonColumn = document.createElement('div');
	buttonColumn.setAttribute("class", "col-xs-2");

	var addSectionButton = document.createElement('button');
	addSectionButton.setAttribute("type", "button");
	addSectionButton.setAttribute("id", "add-section-button" + courseNumber);
	addSectionButton.innerHTML = 'Add Section';
	addSectionButton.addEventListener("click", function() {addSection(timeColumn)});

	buttonColumn.append(addSectionButton);
	courseRow.append(courseColumn);
	courseRow.append(timeColumn);
	courseRow.append(buttonColumn);
	courseList.append(courseRow);

	addSection(timeColumn);
}

function addSection(timeColumn) {
	var row = document.createElement('div');
	row.setAttribute("class", "row");

	var durationColumn = document.createElement('div');
	durationColumn.setAttribute("class", "col-xs-2");
	durationColumn.innerHTML =  'Duration: ' +
		'<select>' +
		'<option value = "lecture">usual</option>' +
		'<option value = "lab">lab</option>' +
		'</select>';

	var time1Column = document.createElement('div');
	time1Column.setAttribute("class", "col-xs-5");
	time1Column.innerHTML = 'TIME1: ' +
		'<select>' +
		'<option value = "mon">MON</option>' +
		'<option value = "tue">TUE</option>' +
		'<option value = "wed">WED</option>' +
		'<option value = "thu">THU</option>' +
		'<option value = "fri">FRI</option>' +
		'</select>';
	time1Column.innerHTML += '<input type = "time">';

	var time2Column = document.createElement('div');
	time2Column.setAttribute("class", "col-xs-5");
	time2Column.innerHTML = 'TIME2: ' +
		'<select>' +
		'<option value = "mon">MON</option>' +
		'<option value = "tue">TUE</option>' +
		'<option value = "wed">WED</option>' +
		'<option value = "thu">THU</option>' +
		'<option value = "fri">FRI</option>' +
		'</select>';
	time2Column.innerHTML += '<input type = "time">';

	row.append(durationColumn);
	row.append(time1Column);
	row.append(time2Column);
	timeColumn.append(row);
}


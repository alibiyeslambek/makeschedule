var courseNumber = 0;

document.getElementById('add-course-button').addEventListener("click", addCourse);
document.getElementById('submit-button').addEventListener("click", submitForm);

function dfs(v, id) {
	if (v.classList.contains('course-name')) v.name = "course[" + id + "][name]";
	if (v.classList.contains('course-must-take')) v.name = "course[" + id + "][must-take]";
	if (v.classList.contains('course-duration')) v.name = "course[" + id + "][duration]";
	if (v.classList.contains('course-credits')) v.name = "course[" + id + "][credits]";
	if (v.classList.contains('section-day1')) v.name = "course[" + id + "][section][][day1]";
	if (v.classList.contains('section-time1')) v.name = "course[" + id + "][section][][time1]";
	if (v.classList.contains('section-day2')) v.name = "course[" + id + "][section][][day2]";
	if (v.classList.contains('section-time2')) v.name = "course[" + id + "][section][][time2]";
	if (v.classList.contains('section-code')) v.name = "course[" + id + "][section][][code]";
	var ch = v.children;
	for (var i = 0; i < ch.length; i++) {
		dfs(ch[i], id);
	}
}

function submitForm() {
	var courseRow = document.getElementsByClassName('course-row');
	for (var i = 1; i < courseRow.length; i++) {
		dfs(courseRow[i], i - 1);
	}

	var form = $('#course-list');
	var data = JSON.stringify($('#course-list').serializeJSON());

	var xhr = new XMLHttpRequest();
	var url = ".";
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
			console.log(xhr.responseText);
    	console.log("guzel");

			var newWindow = window.open();
			newWindow.document.write(xhr.responseText);
		}
	};
	xhr.send(data);
	return false;
}

function addCourse()  {
	if(courseNumber == 10) {
		window.alert("You can add 10 courses at most");
		return;
	}
	courseNumber++;
	var courseRow = document.getElementsByClassName('course-row')[0].cloneNode(true);
	var courseList = document.getElementById('course-list');
	var courseColumn = courseRow.firstElementChild;
	courseRow.hidden = false;
	courseList.append(courseRow);

	var len = courseColumn.children.length;

	var deleteButton = courseColumn.children[len-2];
	var addSectionButton = courseColumn.children[len-1];

	addSectionButton.addEventListener('click', addSection);
	deleteButton.addEventListener("click", deleteCourse);
}

function addSection() {
	var courseRow = this.parentElement.parentElement;
	var timeColumn = courseRow.getElementsByClassName('time-column')[0];

	var sectionRow = document.getElementsByClassName('time-row')[0].cloneNode(true);
	sectionRow.hidden = false;

	timeColumn.append(sectionRow);

	var deleteSectionButton = sectionRow.getElementsByClassName('delete-section-button')[0];
	console.log(deleteSectionButton);
	deleteSectionButton.addEventListener("click", deleteSection);

}

function deleteCourse() {
	courseNumber--;
	var courseRow = this.parentElement.parentElement;
	courseRow.remove();
}

function deleteSection() {
	var sectionRow = this.parentElement.parentElement;
	sectionRow.remove();
}

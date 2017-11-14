var courseNumber = 0;
var sectionsCount = 0;

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

	var status = document.getElementById('status');
	var button = document.getElementById('submit-button');
	button.innerHTML = "Please wait...";
	button.disabled = true;

	var form = $('#course-form');
	var data = JSON.stringify($('#course-form').serializeJSON());

	var xhr = new XMLHttpRequest();
	var url = ".";
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
			status.innerHTML = "<div class='alert alert-success'><strong>Success! </strong>  <a target='_blank' href='/show?id=" + xhr.responseText.toString() + "'>Click</a> to see the schedule</div>";
		} else {
			status.innerHTML = '<div class="alert alert-danger"> <strong> Check your input!</strong></div>';
		}
		button.disabled = false;
		button.innerHTML = "Generate";
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

	addSection(courseRow);
	addSectionButton.addEventListener('click', function() {addSection(courseRow)});
	deleteButton.addEventListener("click", deleteCourse);
}

function addSection(courseRow) {
	if (sectionsCount >= 40) {
			window.alert("No more than 40 sections allowed!");
			return;
	}

	//var courseRow = this.parentElement.parentElement;
	var timeColumn = courseRow.getElementsByClassName('time-column')[0];

	sectionsCount++;

	var sectionRow = document.getElementsByClassName('time-row')[0].cloneNode(true);
	sectionRow.hidden = false;

	timeColumn.append(sectionRow);

	var deleteSectionButton = sectionRow.getElementsByClassName('delete-section-button')[0];
	deleteSectionButton.addEventListener("click", deleteSection);

}

function deleteCourse() {
	courseNumber--;
	var courseRow = this.parentElement.parentElement;
	var timeColumn = courseRow.getElementsByClassName('time-column')[0];
	sectionsCount -= timeColumn.childElementCount;
	courseRow.remove();

}

function deleteSection() {
	sectionsCount--;
	var sectionRow = this.parentElement.parentElement;
	sectionRow.remove();
}

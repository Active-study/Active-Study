// Add this script to your HTML template
document.addEventListener('DOMContentLoaded', function() {
  const classSelect = document.getElementById('classSelect');
  const subjectSelect = document.getElementById('subjectSelect');
  const chapterSelect = document.getElementById('chapterSelect');
  const getDataBtn = document.getElementById('getdata');

  // Load initial classes
  fetch('/get-classes/')
      .then(response => response.json())
      .then(classes => {
          classSelect.innerHTML = classes.map(c => 
              `<option value="${c.id}">${c.class_name}</option>`
          ).join('');
          loadSubjects(classSelect.value);
      });

  // When class changes
  classSelect.addEventListener('change', function() {
      loadSubjects(this.value);
  });

  // When subject changes
  subjectSelect.addEventListener('change', function() {
      loadChapters(this.value);
  });

  function loadSubjects(classId) {
      fetch(`/get-subjects/${classId}/`)
          .then(response => response.json())
          .then(subjects => {
              subjectSelect.innerHTML = subjects.map(s => 
                  `<option value="${s.id}">${s.subject_name}</option>`
              ).join('');
              loadChapters(subjectSelect.value);
          });
  }

  function loadChapters(subjectId) {
      fetch(`/get-chapters/${subjectId}/`)
          .then(response => response.json())
          .then(chapters => {
              chapterSelect.innerHTML = chapters.map(c => 
                  `<option value="${c.id}">${c.chapter_name}</option>`
              ).join('');
          });
  }

  // Handle form submission
  getDataBtn.addEventListener('click', function() {
      const chapterId = chapterSelect.value;
      fetch(`/get-resources/${chapterId}/`)
          .then(response => response.json())
          .then(resources => {
              // Handle the resources (display links/download buttons)
              console.log('Available resources:', resources);
              // Example: display links
              const element = document.getElementById('element');
              element.innerHTML = `
                  ${resources.notes ? `<a href="${resources.notes}" download>Download Notes</a><br>` : ''}
                  ${resources.english_book ? `<a href="${resources.english_book}" download>Download English Book</a><br>` : ''}
                  ${resources.hindi_book ? `<a href="${resources.hindi_book}" download>Download Hindi Book</a><br>` : ''}
                  ${resources.questions ? `<a href="${resources.questions}" download>Download Questions</a><br>` : ''}
                  ${resources.quiz ? `<a href="${resources.quiz}" download>Download Quiz</a><br>` : ''}
              `;
              element.style.display = 'block';
          });
  });
});
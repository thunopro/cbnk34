document.addEventListener('DOMContentLoaded', () => {
    const subjectList = document.getElementById('subjectList');
    const leaderboardBody = document.getElementById('leaderboardBody');
    const currentSubjectTitle = document.getElementById('currentSubjectTitle');
    const totalStudents = document.getElementById('totalStudents');
    const searchInput = document.getElementById('searchInput');
    const noDataMessage = document.getElementById('noDataMessage');

    // Contact Us Elements
    const contactUsBtn = document.getElementById('contactUsBtn');
    const contactModal = document.getElementById('contactModal');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const contactAudio = document.getElementById('contactAudio');

    let allData = {};
    let currentSubject = '';
    let currentSearchTerm = '';

    // Contact Modal Logic
    if (contactUsBtn && contactModal && closeModalBtn && contactAudio) {
        contactUsBtn.addEventListener('click', (e) => {
            e.preventDefault();
            contactModal.classList.remove('hidden');
            contactAudio.currentTime = 0;
            contactAudio.play().catch(err => console.log('Audio auto-play prevented:', err));
        });

        closeModalBtn.addEventListener('click', () => {
            contactModal.classList.add('hidden');
            contactAudio.pause();
        });

        // Close on clicking outside
        contactModal.addEventListener('click', (e) => {
            if (e.target === contactModal) {
                contactModal.classList.add('hidden');
                contactAudio.pause();
            }
        });
    }

    // Fetch data
    fetch('data.json')
        .then(response => response.json())
        .then(data => {
            allData = data;
            initApp();
        })
        .catch(error => {
            console.error('Error loading data:', error);
            leaderboardBody.innerHTML = `<tr><td colspan="10" class="text-center" style="color: #ef4444;">Lỗi tải dữ liệu. Vui lòng thử lại sau.</td></tr>`;
        });

    function initApp() {
        const subjects = Object.keys(allData);
        if (subjects.length === 0) return;

        // Render subjects sidebar
        subjects.forEach((subject, index) => {
            const li = document.createElement('li');
            const studentCount = allData[subject].length;
            li.innerHTML = `
                <span>${subject}</span>
                <span class="count-badge">${studentCount}</span>
            `;
            li.dataset.subject = subject;
            
            li.addEventListener('click', () => {
                // Remove active class
                document.querySelectorAll('.subject-list li').forEach(el => el.classList.remove('active'));
                li.classList.add('active');
                
                // Select subject
                selectSubject(subject);
            });

            subjectList.appendChild(li);

            // Select first subject by default
            if (index === 0) {
                li.classList.add('active');
                selectSubject(subject);
            }
        });

        // Setup search
        searchInput.addEventListener('input', (e) => {
            currentSearchTerm = e.target.value.toLowerCase().trim();
            renderTable();
        });
    }

    function selectSubject(subject) {
        currentSubject = subject;
        currentSubjectTitle.textContent = `Chuyên ${subject}`;
        
        // Reset search when changing subject
        searchInput.value = '';
        currentSearchTerm = '';
        
        renderTable();
    }

    function renderTable() {
        if (!currentSubject || !allData[currentSubject]) return;

        let students = allData[currentSubject];
        
        // Filter by search
        if (currentSearchTerm) {
            students = students.filter(s => 
                (s.FULLNAME && s.FULLNAME.toLowerCase().includes(currentSearchTerm)) ||
                (s.SBD && s.SBD.toString().includes(currentSearchTerm))
            );
        }

        totalStudents.textContent = students.length;

        // Render
        leaderboardBody.innerHTML = '';
        
        if (students.length === 0) {
            noDataMessage.classList.remove('hidden');
        } else {
            noDataMessage.classList.add('hidden');
            
            let htmlRows = '';
            // Only animate the first 20 rows to save performance
            students.forEach((student, index) => {
                const animDelay = index < 20 ? `style="--animation-order: ${index};"` : 'style="animation: none; opacity: 1;"';
                
                // Format numbers safely
                const math = formatScore(student.TONGTOAN);
                const lit = formatScore(student.NGUVAN);
                const eng = formatScore(student.TIENGANH);
                const total = formatScore(student.TONGDT);
                const special = formatScore(student.DIEMCHUYEN);

                htmlRows += `
                    <tr class="rank-${student.RANK}" ${animDelay}>
                        <td class="col-rank">
                            <span class="rank-number">${student.RANK}</span>
                        </td>
                        <td>${student.SBD}</td>
                        <td>
                            <div class="student-name">${student.FULLNAME || 'N/A'}</div>
                        </td>
                        <td>
                            <div class="school-name">${student.TENTRUONG || 'Thí sinh tự do'}</div>
                        </td>
                        <td class="col-score text-right">${math}</td>
                        <td class="col-score text-right">${lit}</td>
                        <td class="col-score text-right">${eng}</td>
                        <td class="col-score text-right">${total}</td>
                        <td class="col-score highlight-score text-right">${special}</td>
                    </tr>
                `;
            });
            leaderboardBody.innerHTML = htmlRows;
        }
    }

    function formatScore(score) {
        if (score === null || score === undefined || score === '') return '-';
        return Number(score).toFixed(2);
    }
});

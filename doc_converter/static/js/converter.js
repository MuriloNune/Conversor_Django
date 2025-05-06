// static/js/converter.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        showLoading();
        
        const formData = new FormData(form);
        
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if(data.task_id) {
                pollConversionStatus(data.task_id);
            }
        })
        .catch(error => {
            hideLoading();
            showError(error.message);
        });
    });
});

function pollConversionStatus(taskId) {
    const statusUrl = `/conversion-status/${taskId}/`;
    
    const poll = setInterval(() => {
        fetch(statusUrl)
        .then(response => response.json())
        .then(data => {
            if(data.status === 'completed') {
                clearInterval(poll);
                window.location.href = '/download/';
            } else if(data.status === 'failed') {
                clearInterval(poll);
                showError(data.message);
            }
        });
    }, 2000);
}
document.addEventListener("DOMContentLoaded", function() {
    const collectForm = document.getElementById('collectMoneyForm');
    const transferForm = document.getElementById('transferMoneyForm');

    if (collectForm) {
        collectForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(collectForm);
            fetch('/collect_money/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            });
        });
    }

    if (transferForm) {
        transferForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(transferForm);
            fetch('/transfer_money/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            });
        });
    }
});

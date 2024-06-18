(function () {
    window.addEventListener('message', function (event) {
        if (event.data.action === 'file-selected') {
            window.opener.postMessage(event.data, '*');
            window.close();
        }
    });
})();

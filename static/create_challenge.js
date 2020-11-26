const form = document.forms[0];
const outputArea = form.querySelector('#output')

const handleCodeResponse = ({ success, output, ...additional }) => {
	outputArea.value = output;
	return { success, ...additional };
}

form.addEventListener('submit', e => {
	e.preventDefault();
	return fetch('/api/create_challenge', { method: 'POST', body: new FormData(form) })
		.then(r => r.json())
		.then(handleCodeResponse)
		.then(({ success, id }) => {
			if (success) window.location = '/c/' + id;
		})
		.catch(console.error);
});

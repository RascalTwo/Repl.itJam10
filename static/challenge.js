const form = document.forms[0];
const submitButton = form.querySelector('#submit-button');
const outputArea = form.querySelector('#output')

form.querySelector('[name="code"]').addEventListener('input', () =>
	submitButton.setAttribute('disabled', 'true')
);

const handleCodeResponse = ({ success, output, ...additional }) => {
	if (success) submitButton.removeAttribute('disabled')
	else submitButton.setAttribute('disabled', 'true')

	outputArea.value = output;
	return { success, ...additional };
}

form.addEventListener('submit', e => {
	e.preventDefault();
	return fetch('/api/run', { method: 'POST', body: new FormData(form) })
		.then(r => r.json())
		.then(handleCodeResponse)
		.catch(console.error);
});

submitButton.addEventListener('click', e =>
	fetch('/api/submit', { method: 'POST', body: new FormData(form) })
		.then(r => r.json())
		.then(handleCodeResponse)
		.then(({ success }) => {
			if (success) window.location = '/c/' + form.id.value;
		})
		.catch(console.error)
)
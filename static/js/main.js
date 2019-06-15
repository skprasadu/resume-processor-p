$(document).ready(function () {
	var input = document.getElementById('uploadResumeFile');
	input.addEventListener('change', function(e) {
		fileName = e.target.files[0].name;
		var formData = new FormData();
		formData.append('file', this.files[0]);

		var retVal = confirm("Do you want to upload Resume? " + fileName);

		if (retVal == true) {
			$.ajax({
				url: '/uploadResume',
				type: 'POST',
				xhrFields: {
					responseType: 'blob'
				},
				xhr: function() {
					var xhr = $.ajaxSettings.xhr();
					if (xhr.upload) {
						/*xhr.upload.addEventListener('progress', function(evt) {
							var percent = (evt.loaded / evt.total) * 100;
							$("#files").find(".progress-bar").width(percent + "%");
						}, false);*/
						$('.loader').css({
							"display": "block"
						});	
					}
					return xhr;
				},
				success: function(data) {
					/*$("#files").children().last().remove();
					$("#files").append($("#fileUploadItemTemplate").tmpl(data));
					$("#uploadFile").closest("form").trigger("reset");*/
					console.log(typeof data);
					console.log("upload successful!");
					//console.log(data);
					$('.loader').css({
						"display": "none"
					});

					var img = document.getElementById('wordCloudBlob');
					var url = window.URL || window.webkitURL;
					img.src = url.createObjectURL(data);

					toggleAllButtons(false);
					fileName = "";
				},
				error: function() {
					/*$("#fileUploadError").removeClass("hide").text("An error occured!");
					$("#files").children().last().remove();
					$("#uploadFile").closest("form").trigger("reset");*/
					console.log("upload error: " + error.name + ": " + error.message);
					$('#progress').html("Failure!<br>" + error.name + ": " + error.message);
					toggleAllButtons(false);
				},
				data: formData,
				cache: false,
				contentType: false,
				processData: false
			});
		}
	});

	$('#uploadResumeFile').inputFileText({
		text: 'Upload Resume File'
	});

	function toggleAllButtons(status) {
		document.getElementById("uploadResumeFile").disabled = status;
	}
});

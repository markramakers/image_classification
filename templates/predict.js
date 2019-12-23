$(document).on("click", ".browse", function() {
  var file = $(this).parents().find(".file");
  file.trigger("click");
});

$('input[type="file"]').change(function(e) {

  var fileName = e.target.files[0].name;

  $("#file").val(fileName);

  var reader = new FileReader();
  reader.onload = function(e) {
    // get loaded data and render thumbnail.
    document.getElementById("preview").src = e.target.result;
  };
  // read the image file as a data URL.
  reader.readAsDataURL(this.files[0]);

  const formData = new FormData()
  formData.append('file', e.target.files[0])
    fetch('/predict', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        t = ""
          for (const property in data) {
              t += "<tr><td>" + property + "</td><td> " + data[property] + "</td></tr>"
          }
          document.getElementById('predictions').innerHTML = "<table>" + t + "</table>"
      })
      .catch(error => {
        console.error(error)
      })
});

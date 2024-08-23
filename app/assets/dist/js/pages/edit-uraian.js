$(document).ready(function () {
    $("#sasaran").prop("disabled", true);
    $("#indikator").prop("disabled", true);

    var checkbox = document.querySelector('input[type="checkbox"]');
    var jabatan_id = document.getElementById("helper").getAttribute("data-name");

    checkbox.addEventListener('change', function () {
        if (checkbox.checked) {
            $("#sasaran").prop("disabled", false);

            var jabatan_id = document.getElementById("helper").getAttribute("data-name");

            // Remove old options
            $('#indikator').find('option').remove();
            $('#sasaran').find('option').remove();

            // Add blank items
            var blank_item1 = '<option value=""> Belum ada pilihan</option>'
            $('#indikator').append(blank_item1);
            var blank_item2 = '<option value=""> Belum ada pilihan</option>'
            $('#sasaran').append(blank_item2);

            $.getJSON(
                '/get-sasaran', {id: jabatan_id},
                function (data) {

                    // Add new items
                    $.each(data, function (key, val) {
                    var option_item = '<option value="' + val.id + '">' + val.name + '</option>'
                    $('#sasaran').append(option_item);
                    });
                });
        } else {
            $("#sasaran").prop("disabled", true);
            $("#indikator").prop("disabled", true);
        }
      });

    $('#sasaran').change(function () {

        $("#indikator").prop("disabled", true);

        var sasaran_id = $('#sasaran').val();

        // Remove old options
        $('#indikator').find('option').remove();

        // Add blank items
        var blank_item = '<option value=""> Belum ada pilihan</option>'
        $('#indikator').append(blank_item);

        $.getJSON(
            '/get-indikator', {id:sasaran_id},
            function (data) {

                // Add new items
                $.each(data, function (key, val) {
                var option_item = '<option value="' + val.id + '">' + val.name + '</option>'
                $('#indikator').append(option_item);
                $("#indikator").prop("disabled", false);
                });
            }
        );
    });

});
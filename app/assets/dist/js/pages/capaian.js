 $(document).ready(function () {
    $("#indikator").prop("disabled", true);
    $("#uraian").prop("disabled", true);
    var jabatan_id = document.getElementById("helper").getAttribute("data-name");

    $.getJSON(
            '/get-sasaran', {id: jabatan_id},
            function (data) {

                // Remove old options
                $('#sasaran').find('option').remove();

                // Add new items
                var blank_item = '<option value=""> Belum ada pilihan</option>'
                $('#sasaran').append(blank_item);
                $.each(data, function (key, val) {
                var option_item = '<option value="' + val.id + '">' + val.name + '</option>'
                $('#sasaran').append(option_item);
                });
            }
        );

    $('#sasaran').change(function () {

        $("#indikator").prop("disabled", true);
        $("#uraian").prop("disabled", true);

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
    $('#indikator').change(function () {

        $("#uraian").prop("disabled", true);

        var indikator_id = $('#indikator').val();

        // Remove old options
        $('#uraian').find('option').remove();

        // Add blank items
        var blank_item = '<option value=""> Belum ada pilihan</option>'
        $('#uraian').append(blank_item);

        $.getJSON(
            '/get-uraian', {id:indikator_id},
            function (data) {

                // Add new items
                $.each(data, function (key, val) {
                var option_item = '<option value="' + val.id + '">' + val.uraian_tugas + '</option>'
                $('#uraian').append(option_item);
                $("#uraian").prop("disabled", false);
                });
            }
        );
    });

    $('#defaultModal').on('hidden.bs.modal', function () {
        location.reload(true);
    })

});
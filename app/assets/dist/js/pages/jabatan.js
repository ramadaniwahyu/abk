 $(document).ready(function () {

    // var jabatan_id = item.id;
    $("#indikator").prop("disabled", true);
    var jabatan_id = document.getElementById("helper").getAttribute("data-name");
    // const queryString = window.location.search;
    // const urlParams = new URLSearchParams(queryString);
    // const jabatan_id = urlParams.get('id');
    // var my_params = { id: jabatan_id};
    // console.log(my_params)

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

    $('#defaultModal').on('hidden.bs.modal', function () {
        location.reload(true);
    })

});
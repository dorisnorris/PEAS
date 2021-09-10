// this will initialize the datatable on the data page

// DATA 
$(document).ready(function() {
    // Setup - add a text input to each footer cell
    $('#test_table tfoot th').each( function () {
        var title = $(this).text();
        $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
    } );
 
    // DataTable
    var table = $('#test_table').DataTable({
        columnDefs: [
            { width: "8px", targets: [0] } // attempting to resize the columns in the datatable; does not work at the moment
        ],
        fixedColumns: true,
        initComplete: function () {

            // Apply the search
            this.api().columns().every( function () {
                var that = this;
 
                $( 'input', this.footer() ).on( 'keyup change clear', function () {
                    if ( that.search() !== this.value ) {
                        that
                            .search( this.value )
                            .draw();
                    }
                } );
            } );
        }
    });

 
} );
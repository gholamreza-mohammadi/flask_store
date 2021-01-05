$(function () {
    $("a.delete_a").click(function (event) {
        event.preventDefault();
        var $this = $(this);
        var tr = $this.closest("tr");
        var id = $this.attr("id");
        var price = parseFloat(tr.find(".price").html());
        var quantity = parseFloat(tr.find(".quantity").html());
        $.ajax({
            type: "POST",
            contentType: "application/json",
            url: "change-shopping-list",
            dataType: "json",
            data: JSON.stringify({ id: id }),
        }).always(function (response) {
            if (response.responseText == "deleted") {
                var $total_price = $("span#total_price");
                var total_price = parseFloat($total_price.html());
                $total_price.html(total_price - price * quantity);
                tr.remove();
            }
        });
    });
});

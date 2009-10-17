$(function() {
    var bindform = function(from) {
        if (!from) from = document;
        $("#delete-book", from).submit(function() {
            $.ajax({
                type: "DELETE",
                url: this.action,
                success: function() {
                    location.href = "/";
                },
                error: function() {
                    alert("エラーです(エラー処理を実装するよう管理者に頼んでください)");
                }
            });
            return false;
        });
        $(".delete-comment", from).submit(function() {
            var self = this;
            $.ajax({
                type: "DELETE",
                url: this.action,
                success: function() {
                    $(self.parentNode.parentNode.parentNode).remove();
                },
                error: function() {
                    alert("エラーです(エラー処理を実装するよう管理者に頼んでください)");
                }
            });
            return false;
        });

        $(".post-comment", from).submit(function() {
            var self = this;
            $(".submit", self)[0].disabled = true;
            $.ajax({
                type: self.method,
                url: self.action,
                data: $(self).serialize(),
                success: function(res) {
                    var item = $("<li>").html(res);
                    $(".comments").append(item);
                    self.body.value = "";
                    bindform(item);
                },
                error: function() {
                    alert("エラーです(エラー処理を実装するよう管理者に頼んでください)");
                },
                complete: function() {
                    $(".submit", self)[0].disabled = false;
                }
            });
            return false;
        });

    };
    bindform();
});
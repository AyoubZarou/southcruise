<script>
    $(function(){
        $("#desired-order-sortable").sortable({stop: (event) => {update_shown_indexes_weights()}});
        $("#desired-startup-order-sortable").sortable({stop: (event) => {update_shown_indexes_weights("", "startup")}})
        $("#desired-company-order-sortable").sortable({stop: (event) => {update_shown_indexes_weights("", "company")}})
        update_shown_indexes_weights("", "startup")
        update_shown_indexes_weights("", "company")
        update_shown_indexes_weights("", "country")
        feather.replace()
    })
</script>
<script>
    $(function(){
        {% include 'js/set_svg.js' %}
    })
</script>
<script>
    $(function(){
        {% include "js/startup_table.js" %}
    })
</script>
<script>
    $(function(){
        {% include "js/charts_script.js" %}
    })
</script>
<div class="block_reg"><p><h1>Регистрация</h1></p>
        <div class="list" >
            <form method="POST" action="/create-user">
                <form method="post" class="person-form">
                    {{ form.hidden_tag() }}
                    <div class="form-group">
                        {{ form.name.label(class="form-label") }}
                        {{ form.name(class="form-input") }}
                    </div>
                    <div class="form-group">
                        {{ form.age.label(class="form-label") }}
                        {{ form.age(class="form-input") }}
                    </div>
                    <div class="form-group">
                        {{ form.main_info.label(class="form-label") }}
                        {{ form.main_info(class="form-input") }}
                    </div>
                    <div>
                        {{ form.submit(class="submit-button") }}
                    </div>
                </form>
        </div>
{% extends "mail_templated/base.tpl" %}

{% block subject %}
Activation Email - Welcome to Our Service
{% endblock %}

{% block html %}
<html>
  <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
    <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 8px; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
      <h2 style="color: #333333;">Hello {{ user.name }},</h2>
      <p style="color: #555555;">Thank you for registering on our platform. Please click the button below to activate your account:</p>
      <div style="text-align: center; margin: 30px 0;">
        <a href="http://127.0.0.1:8000/accounts/api/v1/activation/conform/{{ token }}" style="background-color: #4CAF50; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px;">Activate Account</a>
      </div>
      <p style="color: #888888;">If the button doesn't work, copy and paste this URL into your browser:</p>
      <p style="color: #888888;"><code>http://127.0.0.1:8000/accounts/api/v1/activation/conform/{{ token }}</code></p>
      <hr style="margin-top: 40px; border: none; border-top: 1px solid #eeeeee;">
          <a href="http://127.0.0.1:8000/accounts/api/v1/activation/resend/" style="background-color: #4CAF50; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px;">resend activation link </a>
      <p style="font-size: 12px; color: #aaaaaa;">If you didn’t request this email, please ignore it.</p>
    </div>
  </body>
</html>
{% endblock %}

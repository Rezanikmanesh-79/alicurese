{% extends "mail_templated/base.tpl" %}

{% block subject %}
Password Reset Request - Our Service
{% endblock %}

{% block html %}
<html>
  <body style="font-family: Arial, sans-serif; background-color: #f3f3f3; padding: 20px;">
    <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 10px; padding: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
      <h2 style="color: #333;">Password Reset Requested</h2>
      <p style="color: #555;">You recently requested to reset your password for your account. Click the button below to reset it:</p>
      
      <div style="text-align: center; margin: 30px 0;">
        <a href="http://127.0.0.1:8000/accounts/api/v1/password/confirm/{{ token }}" 
           style="display: inline-block; background-color: #007bff; color: #fff; padding: 12px 25px; text-decoration: none; border-radius: 5px;">
           Reset Password
        </a>
      </div>

      <p style="color: #888;">If you didn’t request this, you can safely ignore this email.</p>
      <p style="color: #888;">Or copy and paste this URL into your browser:</p>
      <p style="color: #aaa;"><code>http://127.0.0.1:8000/accounts/api/v1/password/confirm/{{ token }}</code></p>

      <hr style="margin-top: 40px; border: none; border-top: 1px solid #eee;">
      <p style="font-size: 12px; color: #aaa;">This link will expire in a short time for your security.</p>
    </div>
  </body>
</html>
{% endblock %}

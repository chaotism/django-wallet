set -e

echo "Waiting for mysql..."
while ! nc -z db 3306; do
  sleep 0.1
done
echo "mysql started"

python manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('${API_ADMIN_USERNAME}', '${API_ADMIN_MAIL}', '${API_ADMIN_PASSWORD}')" \
  | python manage.py shell

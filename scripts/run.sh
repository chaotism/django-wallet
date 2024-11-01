set -e

echo "Waiting for mysql..."
while ! nc -z db 3306; do
  sleep 0.1
done
echo "mysql started"

python manage.py runserver "${API_HOST}:${API_PORT}"

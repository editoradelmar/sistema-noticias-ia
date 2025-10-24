# ===== ETAPA 1: BUILD =====
FROM node:18-alpine AS build

WORKDIR /app

# Copiar package.json
COPY package*.json ./

# Instalar dependencias
RUN npm ci

# Copiar código
COPY . .

# Compilar para producción
RUN npm run build

# ===== ETAPA 2: PRODUCCIÓN =====
FROM nginx:alpine AS production

# Copiar archivos compilados
COPY --from=build /app/dist /usr/share/nginx/html

# Copiar configuración nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
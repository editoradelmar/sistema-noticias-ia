// Script para probar ordenamiento alfabético de secciones
// Simula el funcionamiento del código implementado

const secciones = [
  { id: 1, nombre: "Zootecnia" },
  { id: 2, nombre: "Deportes" },
  { id: 3, nombre: "Política" },
  { id: 4, nombre: "Entretenimiento" },
  { id: 5, nombre: "Cultura" },
  { id: 6, nombre: "Ambiente" },
  { id: 7, nombre: "Salud" },
  { id: 8, nombre: "Bienestar" },
  { id: 9, nombre: "Tecnología" }
];

console.log("🔍 ANTES del ordenamiento:");
secciones.forEach(s => console.log(`   ${s.nombre}`));

// Aplicar el mismo ordenamiento que implementamos
const seccionesOrdenadas = secciones.sort((a, b) => 
  a.nombre.localeCompare(b.nombre, 'es', { sensitivity: 'base' })
);

console.log("\n✅ DESPUÉS del ordenamiento alfabético:");
seccionesOrdenadas.forEach(s => console.log(`   ${s.nombre}`));

console.log("\n📋 Resultado esperado en los dropdowns:");
console.log("   Todas las secciones aparecerán en orden alfabético");
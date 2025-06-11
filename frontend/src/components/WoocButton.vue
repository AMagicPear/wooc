<template lang="pug">
    button
        slot
</template>

<style scoped>
button {
  /* margin-block: 60px; */
  padding-inline: 40px;
  padding-block: 8px;
  border-radius: var(--card-border-radius);
  border-style: none;
  background-color: var(--color-tint);
  color: white;
  font-size: 16px;
  font-weight: bolder;
  cursor: pointer;
}

button:hover {
  opacity: 0.8;
}

button:active {
  opacity: 0.6;
}
</style>
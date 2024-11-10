<script setup lang="ts">
const { enabled = true, type = "button" } = defineProps<{
  enabled?: boolean;
  type?: "button" | "submit" | "reset";
}>();
</script>

<template>
  <button
    class="bg-secondary-light dark:bg-secondary-dark text-secondary-content-light dark:text-secondary-content-dark rounded-lg px-4 py-2 text-sm font-bold"
    :class="
      enabled
        ? [
            'dark:hover:bg-secondary-active-dark',
            'hover:bg-secondary-active-light',
          ]
        : []
    "
    :type="type"
    :disabled="!enabled"
  >
    <slot>Button</slot>
  </button>
</template>

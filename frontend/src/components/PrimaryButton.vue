<script setup lang="ts">
const { enabled = true, type = "button" } = defineProps<{
  enabled?: boolean;
  type?: "button" | "submit" | "reset";
}>();
</script>

<template>
  <button
    class="rounded-lg bg-primary-light px-4 py-2 text-sm font-bold text-primary-content-light dark:bg-primary-dark dark:text-primary-content-dark"
    :class="
      enabled
        ? ['dark:hover:bg-primary-active-dark', 'hover:bg-primary-active-light']
        : []
    "
    :type="type"
    :disabled="!enabled"
  >
    <slot>Button</slot>
  </button>
</template>

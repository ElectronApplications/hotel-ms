<script setup lang="ts">
import { toRefs, type ButtonHTMLAttributes } from "vue";

const props = withDefaults(
  defineProps<{
    enabled?: boolean;
    type?: ButtonHTMLAttributes["type"];
  }>(),
  {
    enabled: true,
    type: "button",
  },
);

const { enabled, type } = toRefs(props);
</script>

<template>
  <button
    class="rounded-lg px-4 py-2 text-sm font-bold duration-100"
    :class="[
      enabled
        ? 'bg-primary-light text-primary-content-light hover:bg-primary-active-light dark:bg-primary-dark dark:text-primary-content-dark dark:hover:bg-primary-active-dark'
        : 'bg-primary-disabled-light dark:bg-primary-disabled-dark text-primary-disabled-content-light dark:text-primary-disabled-content-dark',
    ]"
    :type="type"
    :disabled="!enabled"
  >
    <slot>Button</slot>
  </button>
</template>

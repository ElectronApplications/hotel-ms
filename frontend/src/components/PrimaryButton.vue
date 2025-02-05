<script setup lang="ts">
import { toRefs, type ButtonHTMLAttributes } from "vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n({
  messages: {
    en: {
      button: "Button",
    },
    ru: {
      button: "Кнопка",
    },
  },
});

const props = withDefaults(
  defineProps<{
    enabled?: boolean;
    type?: ButtonHTMLAttributes["type"];
  }>(),
  {
    enabled: true,
    type: "button",
  }
);

const { enabled, type } = toRefs(props);
</script>

<template>
  <button
    class="rounded-lg px-4 py-2 text-sm font-bold duration-100"
    :class="[
      enabled
        ? 'bg-primary-light text-primary-content-light hover:bg-primary-active-light dark:bg-primary-dark dark:text-primary-content-dark dark:hover:bg-primary-active-dark'
        : 'bg-primary-disabled-light text-primary-disabled-content-light dark:bg-primary-disabled-dark dark:text-primary-disabled-content-dark',
    ]"
    :type="type"
    :disabled="!enabled"
  >
    <slot>{{ t("button") }}</slot>
  </button>
</template>

<script setup lang="ts">
import TextField from "@/components/TextField.vue";
import { EyeIcon, EyeSlashIcon } from "@heroicons/vue/24/outline";
import { ref, toRefs } from "vue";

const props = withDefaults(
  defineProps<{
    enabled?: boolean;
    name?: string;
    required?: boolean;
    readonly?: boolean;
    placeholder?: string;
  }>(),
  {
    enabled: true,
  },
);

const { enabled, name, required, readonly, placeholder } = toRefs(props);

const model = defineModel<string>();

const showPassword = ref(false);
</script>

<template>
  <div class="relative flex items-center">
    <TextField v-model="model" :enabled="enabled" :type="showPassword ? 'text' : 'password'" :name="name"
      autocomplete="current-password" :required="required" :readonly="readonly" :placeholder="placeholder"
      class="pr-10" />
    <button type="button" class="absolute right-2 text-secondary-active-light dark:text-secondary-active-dark"
      @click="showPassword = !showPassword">
      <EyeIcon v-if="!showPassword" class="h-[24px] w-[24px]" />
      <EyeSlashIcon v-else class="h-[24px] w-[24px]" />
    </button>
  </div>
</template>

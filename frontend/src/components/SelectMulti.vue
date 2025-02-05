<script setup lang="ts">
import { Popover, PopoverButton, PopoverPanel } from "@headlessui/vue";
import { ChevronDownIcon, XMarkIcon } from "@heroicons/vue/24/outline";
import { toRefs } from "vue";

const props = withDefaults(
  defineProps<{
    options: string[];
    placeholder?: string;
    maxTagsShow?: number;
  }>(),
  {
    placeholder: "Select options",
    maxTagsShow: 2,
  },
);

const { options, placeholder, maxTagsShow } = toRefs(props);

const model = defineModel<number[]>();

const emit = defineEmits<{
  updateSelections: [];
}>();

function switchOption(option: number) {
  if (model.value === undefined) {
    model.value = [];
  }

  if (!model.value.includes(option)) {
    model.value = [...model.value, option];
  } else {
    model.value = model.value.filter((x) => x !== option);
  }

  emit("updateSelections");
}
</script>

<template>
  <Popover class="relative">
    <PopoverButton
      class="flex w-full flex-row justify-between rounded-md border-0 bg-surface-light p-2 py-2 shadow-sm ring-1 ring-secondary-light hover:cursor-pointer sm:text-sm/6 dark:bg-surface-dark dark:ring-secondary-active-dark">
      <span v-if="model === undefined || model.length === 0"
        class="text-placeholder-light dark:text-placeholder-dark">{{ placeholder }}</span>
      <div v-else class="flex flex-row space-x-2">
        <div v-for="option in model.slice(0, maxTagsShow)" v-bind:key="option"
          class="flex flex-row space-x-2 rounded-full bg-primary-light p-1 dark:bg-primary-dark">
          <span class="text-nowrap text-sm text-primary-content-light dark:text-primary-content-dark">{{ options[option]
            }}</span>
          <button @click.stop="switchOption(option)">
            <XMarkIcon class="w-[18px] text-primary-content-light dark:text-primary-content-dark" />
          </button>
        </div>
        <span v-if="model.length > maxTagsShow">...</span>
      </div>

      <div class="flex flex-row justify-end">
        <ChevronDownIcon class="w-[18px]" />
      </div>
    </PopoverButton>

    <transition enter-active-class="transition duration-200 ease-out" enter-from-class="translate-y-1 opacity-0"
      enter-to-class="translate-y-0 opacity-100" leave-active-class="transition duration-150 ease-in"
      leave-from-class="translate-y-0 opacity-100" leave-to-class="translate-y-1 opacity-0">
      <PopoverPanel class="absolute left-1/2 z-10 mt-1 -translate-x-1/2">
        <div
          class="flex flex-col overflow-hidden rounded-xl bg-surface-light text-surface-content-light shadow-xl dark:bg-surface-dark dark:text-surface-content-dark">
          <button v-for="[index, option] in options.entries()" v-bind:key="index" class="text-nowrap py-2" :class="[
            model !== undefined && model.includes(index)
              ? 'bg-primary-light text-primary-content-light dark:bg-primary-dark dark:text-primary-content-dark'
              : 'hover:bg-secondary-light hover:text-secondary-content-light dark:hover:bg-secondary-dark dark:hover:text-secondary-content-dark',
          ]" @click="switchOption(index)">
            <span class="px-4">
              {{ option }}
            </span>
          </button>
        </div>
      </PopoverPanel>
    </transition>
  </Popover>
</template>

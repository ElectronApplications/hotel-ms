<script setup lang="ts">
import { PencilIcon, CheckIcon } from "@heroicons/vue/24/outline";
import { ref, toRefs, useTemplateRef, watch, type HTMLAttributes } from "vue";

const props = withDefaults(
  defineProps<{
    text: string;
    textClass?: HTMLAttributes["class"];
    textTag?: string;
  }>(),
  {
    textTag: "span",
  },
);

const { text, textClass, textTag } = toRefs(props);

const emit = defineEmits<{
  updateText: [value: string];
}>();

const editing = ref(false);
const editingText = ref("");

watch(
  text,
  (value) => {
    editingText.value = value;
  },
  {
    immediate: true,
  },
);

const input = useTemplateRef("inputRef");
function inputFocus() {
  setTimeout(() => {
    input.value?.focus();
  }, 20);
}

function updateValue() {
  editing.value = false;
  emit("updateText", editingText.value);
  editingText.value = text.value;
}
</script>

<template>
  <div v-show="!editing" class="flex flex-row items-center" v-bind="$attrs">
    <component :is="textTag" :class="textClass">{{ text }}</component>
    <button
      @click="
        editing = true;
        inputFocus();
      "
      class="px-2"
    >
      <PencilIcon class="h-4 w-4" />
    </button>
  </div>
  <div v-if="editing">
    <form
      class="flex flex-row items-center"
      @submit.prevent="updateValue"
      v-bind="$attrs"
    >
      <input
        type="text"
        ref="inputRef"
        @blur="inputFocus"
        class="w-[250px] bg-inherit outline-none"
        :class="textClass"
        v-model="editingText"
      />
      <button type="submit">
        <CheckIcon class="h-8 w-8" />
      </button>
    </form>
  </div>
</template>

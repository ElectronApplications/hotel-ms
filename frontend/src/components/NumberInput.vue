<script setup lang="ts">
import { ref, toRefs, watch } from "vue";
import { MinusIcon, PlusIcon } from "@heroicons/vue/24/outline";

const props = defineProps<{
  min?: number;
  max?: number;
  name?: string;
  placeholder?: string;
  required?: boolean;
}>();

const { min, max, name, placeholder, required } = toRefs(props);

const emit = defineEmits<{
  updateValue: [];
}>();

const model = defineModel<number>();

const input = ref(model.value?.toString() ?? "1");
watch(model, (value) => {
  input.value = value?.toString() ?? "";
});

function updateModel(newModel: number) {
  if (min.value !== undefined && newModel < min.value) {
    newModel = min.value;
  } else if (max.value !== undefined && newModel > max.value) {
    newModel = max.value;
  }

  model.value = newModel;
  input.value = newModel.toString();
  emit("updateValue");
}

function addModel(value: number) {
  let newModel = model.value ?? min.value ?? 1;
  newModel += value;
  updateModel(newModel);
}

function setModel(value: number) {
  let newModel = isNaN(value) ? (min.value ?? 1) : value;
  updateModel(newModel);
}
</script>

<template>
  <div class="flex flex-row justify-center">
    <button
      @click="addModel(-1)"
      class="h-11 rounded-s-lg border-0 bg-surface-light p-2 py-2 shadow-sm ring-1 ring-secondary-light duration-100 hover:bg-secondary-light dark:bg-surface-dark dark:ring-secondary-active-dark dark:hover:bg-secondary-dark"
    >
      <MinusIcon class="w-3" />
    </button>
    <input
      type="text"
      v-model="input"
      @change="setModel(Number.parseInt(input))"
      class="z-0 block h-11 w-full bg-surface-light p-2 py-2 text-center text-sm text-surface-content-light shadow-sm ring-1 ring-secondary-light dark:bg-surface-dark dark:text-surface-content-dark dark:ring-secondary-active-dark"
      :name="name"
      :placeholder="placeholder"
      :required="required"
    />
    <button
      @click="addModel(+1)"
      class="h-11 rounded-e-lg border-0 bg-surface-light p-2 py-2 shadow-sm ring-1 ring-secondary-light duration-100 hover:bg-secondary-light dark:bg-surface-dark dark:ring-secondary-active-dark dark:hover:bg-secondary-dark"
    >
      <PlusIcon class="w-3" />
    </button>
  </div>
</template>

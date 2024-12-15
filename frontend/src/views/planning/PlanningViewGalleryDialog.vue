<script setup lang="ts">
import PrimaryButton from "@/components/PrimaryButton.vue";
import TextField from "@/components/TextField.vue";
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionChild,
  TransitionRoot,
} from "@headlessui/vue";
import axios from "axios";
import { ref, toRefs } from "vue";

// TODO: modal dialog could be its own actual component (could also make ExpandableImage use it)

const props = defineProps<{
  open: boolean;
}>();

const { open } = toRefs(props);

const galleryName = ref("");

const emit = defineEmits<{
  close: [];
  createGallery: [gallery: number];
}>();

async function createGallery() {
  const { id }: { id: number } = (
    await axios.post("/api/gallery/", {
      name: galleryName.value,
    })
  ).data;

  emit("createGallery", id);
}
</script>

<template>
  <TransitionRoot appear :show="open" as="template">
    <Dialog as="div" @close="emit('close')" class="relative z-10">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black bg-opacity-50" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div
          class="flex min-h-full items-center justify-center p-4 text-center"
        >
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel
              class="w-full max-w-md transform overflow-hidden rounded-2xl bg-surface-light p-6 text-left align-middle shadow-xl transition-all dark:bg-surface-dark"
            >
              <DialogTitle as="h3" class="text-lg font-medium leading-6">
                Create new gallery
              </DialogTitle>

              <TextField
                v-model="galleryName"
                placeholder="Gallery name"
                class="mt-4"
                @keyup.enter="if (galleryName !== '') createGallery();"
              />

              <PrimaryButton
                class="mt-4"
                :enabled="galleryName !== ''"
                @click="createGallery"
                >Create</PrimaryButton
              >
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup lang="ts">
import EditableLabel from "@/components/EditableLabel.vue";
import ExpandableImage from "@/components/ExpandableImage.vue";
import router from "@/router";
import { useAuthStore } from "@/stores/auth";
import type { Gallery } from "@/types";
import { CheckIcon, XMarkIcon } from "@heroicons/vue/24/outline";
import axios from "axios";
import { storeToRefs } from "pinia";
import { computed, onMounted, ref, useTemplateRef } from "vue";
import { useRoute } from "vue-router";

const authStore = useAuthStore();
const { currentUser } = storeToRefs(authStore);
const canEdit = computed(
  () =>
    currentUser.value?.role === "planning" ||
    currentUser.value?.role === "admin",
);

const route = useRoute();
const galleryId = Number.parseInt(route.params.id as string);

const gallery = ref<Gallery>();

async function fetchGallery() {
  gallery.value = (await axios.get(`/api/gallery/${galleryId}/`)).data;
}

async function changeGalleryName(newName: string) {
  if (gallery.value?.name !== newName) {
    await axios.put(`/api/gallery/${galleryId}/`, {
      name: newName,
    });
    await fetchGallery();
  }
}

async function deleteImage(image: number) {
  await axios.delete(`/api/gallery/${galleryId}/${image}/`);
  await fetchGallery();
}

const pictures = useTemplateRef("picturesRef");

async function uploadImages() {
  const pictureFiles = pictures.value?.files;

  if (pictureFiles) {
    const formData = new FormData();
    for (let i = 0; i < pictureFiles.length; i++) {
      formData.append("images", pictureFiles[i]);
    }
    await axios.post(`/api/gallery/${galleryId}/upload/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    await fetchGallery();
    return true;
  } else {
    return false;
  }
}

async function deleteGallery() {
  await axios.delete(`/api/gallery/${galleryId}/`);
  router.push("/");
}

onMounted(() => {
  fetchGallery();
});
</script>

<template>
  <main class="container mx-auto pt-4">
    <span class="text-center text-2xl font-bold lg:text-start">
      Gallery {{ galleryId }}
    </span>
    <div v-if="gallery !== undefined" class="pt-2">
      <div v-if="canEdit" class="flex flex-row items-center space-x-2">
        <button class="rounded-md bg-red-500 p-[4px]" @click="deleteGallery">
          <XMarkIcon class="h-[24px] w-[24px] text-white" />
        </button>
        <EditableLabel
          :text="gallery.name"
          as="h1"
          textClass="text-center text-4xl font-extrabold lg:text-start"
          @updateText="(value) => changeGalleryName(value)"
        />
      </div>
      <h1 v-else class="pt-2 text-center text-4xl font-extrabold lg:text-start">
        {{ gallery.name }}
      </h1>

      <div
        class="flex flex-col items-center space-y-2 pt-4 lg:flex-row lg:items-start lg:space-x-2 lg:space-y-0"
      >
        <div
          v-for="image in gallery.images"
          v-bind:key="image.id"
          class="relative"
        >
          <ExpandableImage
            imgClass="rounded-xl w-[400px] h-[300px] object-cover"
            :src="image.image"
          />
          <button
            class="absolute left-2 top-2 rounded-md bg-red-500 p-[4px]"
            @click="deleteImage(image.id)"
          >
            <XMarkIcon class="h-[24px] w-[24px] text-white" />
          </button>
        </div>
      </div>

      <form class="space-y-1 pt-4" @submit.prevent="uploadImages">
        <label class="block text-sm font-semibold" for="pictures"
          >Upload images</label
        >
        <div class="flex flex-row items-center justify-start space-x-1">
          <input
            class="w-[250px] cursor-pointer rounded-lg bg-secondary-light text-sm font-medium text-secondary-content-light file:border-0 file:bg-primary-light file:px-4 file:py-2 file:text-primary-content-light file:duration-100 file:hover:bg-primary-active-light dark:bg-secondary-dark dark:text-secondary-content-dark dark:file:bg-primary-dark dark:file:text-primary-content-dark dark:file:hover:bg-primary-active-dark"
            type="file"
            name="pictures"
            ref="picturesRef"
            multiple
          />
          <button type="submit">
            <CheckIcon class="h-6 w-6" />
          </button>
        </div>
      </form>
    </div>
  </main>
</template>

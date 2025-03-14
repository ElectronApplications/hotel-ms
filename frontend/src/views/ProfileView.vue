<script setup lang="ts">
import { RouterLink } from "vue-router";
import { CheckIcon } from "@heroicons/vue/24/outline";
import SurfaceCard from "@/components/SurfaceCard.vue";
import DefaultProfileImage from "@/assets/default-profile.png";
import { useAuthentication } from "@/composables/auth";
import router from "@/router";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import SecondaryButton from "@/components/SecondaryButton.vue";
import ExpandableImage from "@/components/ExpandableImage.vue";
import EditableLabel from "@/components/EditableLabel.vue";
import axios from "axios";
import { useTemplateRef } from "vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n({
  messages: {
    en: {
      profileInformation: "Profile information",
      yourRole: "Your role: {role}",
      uploadProfilePicture: "Upload new profile picture",
      logout: "Log out",
      changePassword: "Change password",
    },
    ru: {
      profileInformation: "Информация о профиле",
      yourRole: "Ваша роль: {role}",
      uploadProfilePicture: "Загрузить новую фотографию пользователя",
      logout: "Выйти",
      changePassword: "Сменить пароль",
    },
  },
});

const authStore = useAuthStore();
const { currentUser } = storeToRefs(authStore);

async function changeName(value: string) {
  if (value !== currentUser.value?.name) {
    await axios.put("/api/user/update-self/", {
      name: value,
    });
    authStore.updateUserInfo();
  }
}

const picture = useTemplateRef("pictureRef");

async function changeProfilePicture(): Promise<boolean> {
  const pictureFile = picture.value?.files;

  if (pictureFile && pictureFile[0]) {
    const formData = new FormData();
    formData.append("picture", pictureFile[0]);
    await axios.put("/api/user/update-self/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  } else {
    await axios.put("/api/user/update-self/", {
      picture: null,
    });
  }
  authStore.updateUserInfo();
  return true;
}

useAuthentication((isAuthenticated) => {
  if (!isAuthenticated) {
    router.push("/login");
  }
});
</script>

<template>
  <main class="container mx-auto pt-4">
    <h1 class="text-center text-4xl font-extrabold lg:text-start">
      {{ t("profileInformation") }}
    </h1>
    <SurfaceCard class="mt-4 flex flex-col items-center lg:flex-row lg:items-start">
      <ExpandableImage
        imgClass="rounded-full w-[250px] h-[250px] object-cover"
        :src="currentUser?.picture ?? DefaultProfileImage"
        :alt="currentUser?.name"
      />
      <div class="flex flex-col ps-0 pt-4 text-center lg:ps-8 lg:text-start">
        <EditableLabel
          class="justify-center lg:justify-start"
          @updateText="changeName"
          as="h2"
          :text="currentUser?.name ?? ''"
          textClass="text-4xl font-extrabold"
        />

        <h2 class="pt-2 text-xl font-semibold">
          {{ currentUser?.phone_number }}
        </h2>
        <span class="pt-2" v-if="currentUser?.role !== 'client'">
          {{ t("yourRole", { role: currentUser?.role }) }}
        </span>

        <form class="space-y-1 pt-4" @submit.prevent="changeProfilePicture">
          <label class="block text-sm font-semibold" for="picture">{{
            t("uploadProfilePicture")
          }}</label>
          <div class="flex flex-row items-center justify-center space-x-1 lg:justify-start">
            <input
              class="w-[250px] cursor-pointer rounded-lg bg-secondary-light text-sm font-medium text-secondary-content-light file:border-0 file:bg-primary-light file:px-4 file:py-2 file:text-primary-content-light file:duration-100 file:hover:bg-primary-active-light dark:bg-secondary-dark dark:text-secondary-content-dark dark:file:bg-primary-dark dark:file:text-primary-content-dark dark:file:hover:bg-primary-active-dark"
              type="file"
              name="picture"
              ref="pictureRef"
            />
            <button type="submit">
              <CheckIcon class="h-6 w-6" />
            </button>
          </div>
        </form>
      </div>
      <div class="flex flex-row justify-end pt-8 lg:grow lg:pt-0">
        <div class="flex flex-col gap-2">
          <SecondaryButton class="w-[250px]" @click="authStore.logout">{{
            t("logout")
          }}</SecondaryButton>
          <RouterLink to="/change-password">
            <SecondaryButton class="w-[250px]">{{ t("changePassword") }}</SecondaryButton>
          </RouterLink>
        </div>
      </div>
    </SurfaceCard>
  </main>
</template>

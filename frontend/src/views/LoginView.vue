<script setup lang="ts">
import SurfaceCard from "@/components/SurfaceCard.vue";
import BrandIcon from "@/assets/brand-icon.svg";
import router from "@/router";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import { onBeforeMount, ref } from "vue";
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from "@headlessui/vue";
import PrimaryButton from "@/components/PrimaryButton.vue";
import TextField from "@/components/TextField.vue";
import PasswordTextField from "@/components/PasswordTextField.vue";

const authStore = useAuthStore();
const { currentUser } = storeToRefs(authStore);

const login_phone_number = ref("");
const login_password = ref("");
const login_error = ref<string>();

const register_phone_number = ref("");
const register_password = ref("");
const register_confirm_password = ref("");
const register_error = ref<string>();

async function loginSubmit() {
  const result = await authStore.login(
    login_phone_number.value,
    login_password.value,
  );

  if (result) {
    router.push("/profile");
    return true;
  } else {
    login_error.value = "Incorrect phone number or password";
    return false;
  }
}

async function registerSubmit() {
  if (register_password.value !== register_confirm_password.value) {
    register_error.value = "Passwords do not match";
    return false;
  }
}

onBeforeMount(() => {
  if (currentUser.value !== undefined) {
    router.push("/profile");
  }
});
</script>

<template>
  {{ currentUser }}
  <main class="container mx-auto flex justify-center pt-2">
    <SurfaceCard class="flex flex-col items-center">
      <BrandIcon class="scale-150" />

      <div class="pt-6">
        <TabGroup>
          <TabList
            class="flex w-[300px] flex-row space-x-1 rounded-xl bg-primary-light p-1 dark:bg-primary-dark"
          >
            <Tab v-slot="{ selected }" class="basis-1/2 outline-none"
              ><button
                class="w-full rounded-lg py-2"
                :class="[
                  selected
                    ? 'bg-surface-light text-surface-content-light shadow dark:bg-surface-dark dark:text-surface-content-dark'
                    : 'text-primary-content-light hover:bg-primary-active-light dark:text-primary-content-dark dark:hover:bg-primary-active-dark',
                ]"
              >
                Login
              </button></Tab
            >

            <Tab v-slot="{ selected }" class="basis-1/2 outline-none"
              ><button
                class="w-full rounded-lg py-2"
                :class="[
                  selected
                    ? 'bg-surface-light text-surface-content-light shadow dark:bg-surface-dark dark:text-surface-content-dark'
                    : 'text-primary-content-light hover:bg-primary-active-light dark:text-primary-content-dark dark:hover:bg-primary-active-dark',
                ]"
              >
                Register
              </button></Tab
            >
          </TabList>

          <TabPanels class="pt-4">
            <TabPanel>
              <form class="space-y-4" @submit.prevent="loginSubmit">
                <div>
                  <label for="phone_number" class="block text-sm/6 font-medium"
                    >Phone number</label
                  >
                  <TextField
                    class="mt-2"
                    v-model="login_phone_number"
                    name="phone_number"
                    type="tel"
                    autocomplete="tel"
                    :required="true"
                  />
                </div>
                <div>
                  <label for="password" class="block text-sm/6 font-medium"
                    >Password</label
                  >
                  <PasswordTextField
                    class="mt-2"
                    v-model="login_password"
                    name="password"
                    :required="true"
                  />
                </div>
                <div v-if="login_error">
                  <span class="text-primary-light dark:text-primary-dark">{{
                    login_error
                  }}</span>
                </div>
                <div>
                  <PrimaryButton type="submit" class="w-full">
                    Sign in
                  </PrimaryButton>
                </div>
              </form>
            </TabPanel>

            <TabPanel>
              <form class="space-y-4" @submit.prevent="registerSubmit">
                <div>
                  <label for="phone_number" class="block text-sm/6 font-medium"
                    >Phone number</label
                  >
                  <TextField
                    class="mt-2"
                    v-model="register_phone_number"
                    name="phone_number"
                    type="tel"
                    autocomplete="tel"
                    :required="true"
                  />
                </div>
                <div>
                  <label for="password" class="block text-sm/6 font-medium"
                    >Password</label
                  >
                  <PasswordTextField
                    class="mt-2"
                    v-model="register_password"
                    name="password"
                    :required="true"
                  />
                </div>
                <div>
                  <label
                    for="confirm-password"
                    class="block text-sm/6 font-medium"
                    >Confirm password</label
                  >
                  <PasswordTextField
                    class="mt-2"
                    v-model="register_confirm_password"
                    name="confirm-password"
                    :required="true"
                  />
                </div>
                <div v-if="register_error">
                  <span class="text-primary-light dark:text-primary-dark">{{
                    register_error
                  }}</span>
                </div>
                <div>
                  <PrimaryButton type="submit" class="w-full">
                    Sign up
                  </PrimaryButton>
                </div>
              </form>
            </TabPanel>
          </TabPanels>
        </TabGroup>
      </div>
    </SurfaceCard>
  </main>
</template>

<script setup lang="ts">
import DefaultProfileImage from "@/assets/default-profile.png";
import EditableLabel from "@/components/EditableLabel.vue";
import ExpandableImage from "@/components/ExpandableImage.vue";
import PrimaryButton from "@/components/PrimaryButton.vue";
import TextField from "@/components/TextField.vue";
import { useAuthentication, useUserRole } from "@/composables/auth";
import router from "@/router";
import { type Client } from "@/types";
import { XMarkIcon } from "@heroicons/vue/24/outline";
import axios from "axios";
import { debounce } from "lodash";
import { onMounted, ref, watch } from "vue";

const clients = ref<Client[]>([]);

const searchKey = ref("");
watch(searchKey, () => {
  debouncedFetchClients();
});

async function fetchClients() {
  clients.value = (
    await axios.get("/api/client/", {
      params: {
        search: searchKey.value,
      },
    })
  ).data;
}
const debouncedFetchClients = debounce(fetchClients, 200);

async function changeClientName(client: Client, newName: string) {
  if (client.name !== newName) {
    await axios.put(`/api/client/${client.id}/`, {
      name: newName,
    });
    await fetchClients();
  }
}

async function changeClientPhoneNumber(client: Client, newPhoneNumber: string) {
  if (client.phone_number !== newPhoneNumber) {
    await axios.put(`/api/client/${client.id}/`, {
      phone_number: newPhoneNumber,
    });
    await fetchClients();
  }
}

async function deleteClient(client: Client) {
  await axios.delete(`/api/client/${client.id}/`);
  await fetchClients();
}

const newClientName = ref("");
const newClientPhoneNumber = ref("");

async function createClient(): Promise<boolean> {
  if (newClientName.value === "" || newClientPhoneNumber.value === "") {
    return false;
  }

  await axios.post("/api/client/", {
    name: newClientName.value,
    phone_number: newClientPhoneNumber.value,
  });
  await fetchClients();

  newClientName.value = "";
  newClientPhoneNumber.value = "";

  return true;
}

onMounted(async () => {
  await fetchClients();
});

useAuthentication((isAuthenticated) => {
  if (!isAuthenticated) {
    router.push("/login");
  }
});

useUserRole((role) => {
  if (role !== "reception" && role !== "admin") {
    router.push("/profile");
  }
});
</script>

<template>
  <main class="container mx-auto pt-4">
    <div class="flex flex-col space-y-4 lg:flex-row lg:space-x-4 lg:space-y-0">
      <h1 class="text-center text-4xl font-extrabold lg:text-start">
        Hotel clients
      </h1>
      <div class="basis-1/3 px-4 lg:px-0">
        <TextField
          placeholder="Search"
          v-model="searchKey"
          @keyup.enter="fetchClients()"
        />
      </div>
    </div>
    <div
      class="mt-4 rounded-3xl bg-slate-100 px-0 py-6 text-surface-content-light shadow-md dark:bg-secondary-dark dark:text-surface-content-dark"
    >
      <form id="createClientForm" @submit.prevent="createClient" />

      <table
        class="w-full table-auto bg-slate-100 text-center dark:bg-secondary-dark"
      >
        <thead
          class="border-b border-secondary-light dark:border-secondary-active-dark"
        >
          <tr>
            <th></th>
            <th class="py-2">Name</th>
            <th class="py-2">Phone number</th>
            <th class="py-2">Role</th>
            <th class="py-2">Profile image</th>
          </tr>
        </thead>
        <tbody class="bg-surface-light dark:bg-surface-dark">
          <tr v-for="client in clients" v-bind:key="client.id">
            <td
              class="border-b border-secondary-light py-2 dark:border-secondary-active-dark"
            >
              <button
                class="rounded-md bg-red-500 p-[4px]"
                v-if="client.role === 'client'"
                @click="deleteClient(client)"
              >
                <XMarkIcon class="h-[24px] w-[24px] text-white" />
              </button>
            </td>
            <td
              class="border-b border-secondary-light py-6 dark:border-secondary-active-dark"
            >
              <EditableLabel
                v-if="client.role === 'client'"
                class="justify-center"
                :text="client.name"
                @updateText="(value) => changeClientName(client, value)"
              />
              <span v-if="client.role !== 'client'">
                {{ client.name }}
              </span>
            </td>
            <td
              class="border-b border-secondary-light py-6 dark:border-secondary-active-dark"
            >
              <EditableLabel
                v-if="client.role === 'client'"
                class="justify-center"
                :text="client.phone_number"
                @updateText="(value) => changeClientPhoneNumber(client, value)"
              />
              <span v-if="client.role !== 'client'">
                {{ client.phone_number }}
              </span>
            </td>
            <td
              class="border-b border-secondary-light py-6 dark:border-secondary-active-dark"
            >
              {{ client.role }}
            </td>
            <td
              class="border-b border-secondary-light py-2 dark:border-secondary-active-dark"
            >
              <ExpandableImage
                imgClass="w-[64px]"
                :src="client.picture ?? DefaultProfileImage"
                :alt="client.name"
              />
            </td>
          </tr>

          <tr>
            <td
              class="border-b border-secondary-light py-2 dark:border-secondary-active-dark"
            ></td>
            <td
              class="border-b border-secondary-light py-6 dark:border-secondary-active-dark"
            >
              <div class="inline-block w-[100px] lg:w-[250px]">
                <TextField
                  placeholder="Client's name"
                  v-model="newClientName"
                  form="createClientForm"
                />
              </div>
            </td>
            <td
              class="border-b border-secondary-light py-6 dark:border-secondary-active-dark"
            >
              <div class="inline-block w-[100px] lg:w-[250px]">
                <TextField
                  placeholder="Client's phone number"
                  v-model="newClientPhoneNumber"
                  form="createClientForm"
                />
              </div>
            </td>
            <td
              class="border-b border-secondary-light py-6 dark:border-secondary-active-dark"
            >
              client
            </td>
            <td
              class="border-b border-secondary-light py-6 dark:border-secondary-active-dark"
            >
              <PrimaryButton form="createClientForm" type="submit"
                >Create new client</PrimaryButton
              >
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </main>
</template>

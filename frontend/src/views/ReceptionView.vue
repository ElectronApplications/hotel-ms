<script setup lang="ts">
import DefaultProfileImage from "@/assets/default-profile.png";
import EditableLabel from "@/components/EditableLabel.vue";
import ExpandableImage from "@/components/ExpandableImage.vue";
import PrimaryButton from "@/components/PrimaryButton.vue";
import TableCard from "@/components/TableCard.vue";
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

    <TableCard
      :columns="[
        { name: 'delete', display: '' },
        { name: 'name', display: 'Name' },
        { name: 'phone', display: 'Phone number' },
        { name: 'role', display: 'Role' },
        { name: 'image', display: 'Profile image' },
      ]"
      :rows="clients"
      :extraFormRow="{ formName: 'createClientForm', formSubmit: createClient }"
    >
      <template #delete="item">
        <button
          class="rounded-md bg-red-500 p-[4px]"
          v-if="!item.isFormRow && item.data.role === 'client'"
          @click="deleteClient(item.data)"
        >
          <XMarkIcon class="h-[24px] w-[24px] text-white" />
        </button>
      </template>

      <template #name="item">
        <template v-if="!item.isFormRow">
          <EditableLabel
            v-if="item.data.role === 'client'"
            class="justify-center"
            :text="item.data.name"
            @updateText="(value) => changeClientName(item.data, value)"
          />
          <span v-else>
            {{ item.data.name }}
          </span>
        </template>
        <div v-else class="inline-block w-[100px] lg:w-[250px]">
          <TextField
            placeholder="Client's name"
            v-model="newClientName"
            form="createClientForm"
          />
        </div>
      </template>

      <template #phone="item">
        <template v-if="!item.isFormRow">
          <EditableLabel
            v-if="item.data.role === 'client'"
            class="justify-center"
            :text="item.data.phone_number"
            @updateText="(value) => changeClientPhoneNumber(item.data, value)"
          />
          <span v-else>
            {{ item.data.phone_number }}
          </span>
        </template>
        <div v-else class="inline-block w-[100px] lg:w-[250px]">
          <TextField
            placeholder="Client's phone number"
            v-model="newClientPhoneNumber"
            form="createClientForm"
          />
        </div>
      </template>

      <template #role="item">
        <span v-if="!item.isFormRow">
          {{ item.data.role }}
        </span>
        <span v-else> client </span>
      </template>

      <template #image="item">
        <ExpandableImage
          v-if="!item.isFormRow"
          imgClass="w-[64px]"
          :src="item.data.picture ?? DefaultProfileImage"
          :alt="item.data.name"
        />
        <PrimaryButton v-else form="createClientForm" type="submit"
          >Create new client</PrimaryButton
        >
      </template>
    </TableCard>
  </main>
</template>

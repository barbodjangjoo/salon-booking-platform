"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import api from "@/lib/api/client";
import { saveTokens } from "@/lib/auth";

export default function AuthPage() {
  const router = useRouter();

  const [username, setUsername] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const handleLogin = async (
    e: React.FormEvent
  ) => {
    e.preventDefault();

    try {
      setLoading(true);
      setError("");

      const res = await api.post(
        "/core/token/",
        {
          username,
          password,
        }
      );

      saveTokens(
        res.data.access,
        res.data.refresh
      );

      router.push("/booking");
    } catch {
      setError(
        "نام کاربری یا رمز عبور اشتباه است"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-[#0B0B0B] px-6 text-white">
      <div className="w-full max-w-md rounded-3xl border border-white/10 bg-white/[0.03] p-8">
        <h1 className="mb-8 text-center text-3xl font-semibold">
          ورود
        </h1>

        <form
          onSubmit={handleLogin}
          className="space-y-5"
        >
          <input
            value={username}
            onChange={(e) =>
              setUsername(
                e.target.value
              )
            }
            placeholder="نام کاربری"
            className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 outline-none"
          />

          <input
            type="password"
            value={password}
            onChange={(e) =>
              setPassword(
                e.target.value
              )
            }
            placeholder="رمز عبور"
            className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 outline-none"
          />

          {error && (
            <p className="text-sm text-red-400">
              {error}
            </p>
          )}

          <button
            disabled={loading}
            className="w-full rounded-xl bg-[#D4B483] py-3 font-medium text-black"
          >
            {loading
              ? "در حال ورود..."
              : "ورود"}
          </button>
        </form>
      </div>
    </main>
  );
}
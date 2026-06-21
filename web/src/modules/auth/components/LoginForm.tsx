import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  loginSchema,
  type LoginFormData,
} from "../services/loginSchema";
import styles from "./LoginForm.module.scss";
import { Link } from 'react-router-dom';

type Props = {
  onSubmit: (
    data: LoginFormData
  ) => Promise<void>;
};

export default function LoginForm({
  onSubmit,
}: Props) {
  const {
    register,
    handleSubmit,
    formState: {
      errors,
      isSubmitting,
    },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  return (
    <>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className={styles.field}>
          <label>Email</label>
          <input
            type="email"
            autoComplete="email"
            {...register("email")}
          />
          <p className={styles.error}>
            {errors.email?.message}
          </p>
        </div>
        <div className={styles.field}>
          <label>Password</label>
          <input
            type="password"
            autoComplete="current-password"
            {...register("password")}
          />
          <p className={styles.error}>
            {errors.password?.message}
          </p>
        </div>
        <button
          type="submit"
          disabled={isSubmitting}
        >
          {isSubmitting
            ? "Logging in..."
            : "Login"}
        </button>
      </form>
      <div className={styles.register}>
        <p>Don't have an account? <Link to="/register">Register here</Link></p>
      </div>
    </>
  );
}
